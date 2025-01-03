import discord
import asyncio
from colorama import Fore, init, Style

def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"역할 삭제됨: {role.name}")
                    await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"역할 삭제 중 오류 발생: {role.name}")
            except discord.HTTPException:
                print_error(f"역할을 삭제할 수 없음: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"역할 생성됨 {role.name}")
                await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"역할 생성 중 오류 발생: {role.name}")
            except discord.HTTPException:
                print_error(f"역할을 생성할 수 없음: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"채널 삭제됨: {channel.name}")
                await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"채널 삭제 중 오류 발생: {channel.name}")
            except discord.HTTPException:
                print_error(f"채널을 삭제할 수 없음: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        for channel in channels:
            try:
                # 카테고리가 이미 존재하는지 확인
                existing_category = discord.utils.get(guild_to.categories, name=channel.name)
                if existing_category:
                    print(f"카테고리 '{channel.name}' 이미 존재함. 건너뜁니다.")
                    continue

                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    if key is not None:  # role이 None인 경우를 체크
                        role = discord.utils.get(guild_to.roles, name=key.name)
                        if role:  # 역할이 존재하는 경우만 추가
                            overwrites_to[role] = value

                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to
                )
                await new_channel.edit(position=channel.position)
                print_add(f"카테고리 생성됨: {channel.name}")
                await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"카테고리 생성 중 권한 오류: {channel.name}")
            except discord.HTTPException:
                print_error(f"카테고리 생성 중 HTTP 오류: {channel.name}")
            except Exception as e:
                print_error(f"기타 오류 발생: {str(e)}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"채널 {channel_text.name}에 카테고리가 없음!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"텍스트 채널 생성됨: {channel_text.name}")
                await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"텍스트 채널 생성 중 오류 발생: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"텍스트 채널을 생성할 수 없음: {channel_text.name}")
            except:
                print_error(f"텍스트 채널 생성 중 오류 발생: {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"채널 {channel_voice.name}에 카테고리가 없음!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"음성 채널 생성됨: {channel_voice.name}")
                await asyncio.sleep(1)  # 딜레이 1초
            except discord.Forbidden:
                print_error(f"음성 채널 생성 중 오류 발생: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"음성 채널을 생성할 수 없음: {channel_voice.name}")
            except:
                print_error(f"음성 채널 생성 중 오류 발생: {channel_voice.name}")